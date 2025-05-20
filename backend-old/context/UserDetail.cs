using System.ComponentModel.DataAnnotations;
using BuildingBlock.Core.Permissions.Models;
using RSG.Biovision.Domain.Entities.Interfaces;
using RSG.Biovision.Domain.Enums;

namespace RSG.Biovision.Domain.Entities;


public class UserDetail : MainEntity, IHasCompany
{
    [MaxLength(255)]
    public string? FirstNameAr { get; set; }
    [Required] [MaxLength(255)]
    public string FirstNameEn { get; set; }
    [MaxLength(255)]
    public string? LastNameAr { get; set; }
    [Required] [MaxLength(255)]
    public string LastNameEn { get; set; } = null!;

    public string? GovId { get; set; } = null!;
    public string? Code { get; set; }
    public string? Email { get; set; }
    public string? Phone { get; set; }
    public int? ContractedWorkHours { get; set; }
    public bool ContractedOverTime { get; set; } = false;
    public DateTime? DateOfBirth { get; set; }
    public Gender Gender { get; set; } = Gender.Male;
    public DateTime JoiningDate { get; set; }
    public EmploymentType? EmploymentType { get; set; } = Enums.EmploymentType.FullTime;
    public bool CanLogin { get; set; } = true;

    public Guid? CountryId { get; set; }
    public Guid CompanyId { get; set; }
    public Guid UserId { get; set; }
    public Guid? ParentId { get; set; }
    public Guid? RegionId { get; set; }
    public Guid? NationalityId { get; set; }
    public Guid? PositionId { get; set; }
    public Guid? MainContractorId { get; set; }
    public Guid? SubContractorId { get; set; }
    public Guid? EmployeeId { get; set; }
    
    public Country? Country { get; set; }
    public Company Company { get; set; } = null!;
    public User User { get; set; } = null!;
    public AttendanceType AttendanceType { get; set; } = AttendanceType.Schedule;
    public SubContractor? Parent { get; set; } = null!;
    public Region? Region { get; set; }
    public Nationality? Nationality { get; set; }
    public Position? Position { get; set; } = null!;

    // Keep existing relationships but make virtual
    public virtual MainContractor? MainContractor { get; set; }
    public virtual SubContractor? SubContractor { get; set; }
    public virtual Employee? Employee { get; set; }
    public virtual ICollection<MainContractorProject> MainContractorProjects { get; set; } = new List<MainContractorProject>();
    public virtual ICollection<Project> Projects { get; set; } = new List<Project>();
    
}