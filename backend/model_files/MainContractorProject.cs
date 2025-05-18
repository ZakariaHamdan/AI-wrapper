using System.ComponentModel.DataAnnotations.Schema;

namespace RSG.Biovision.Domain.Entities;

public class MainContractorProject : MainEntity
{
    public Guid? MainContractorId { get; set; }
    public Guid ProjectId { get; set; }

    public MainContractor MainContractor { get; set; } = null!;
    public Project Project { get; set; } = null!;
}