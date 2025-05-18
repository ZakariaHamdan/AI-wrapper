using System.ComponentModel.DataAnnotations;
using BuildingBlock.Core.Domain.Abstractions;
using RSG.Biovision.Domain.Enums;

namespace RSG.Biovision.Domain.Entities;

public class City : MainEntity
{
    [MaxLength(255)]
    public string? NameAr { get; set; }
    
    [Required] [MaxLength(255)]
    public string NameEn { get; set; }
    
    public Guid? CountryId { get; set; }

    
    
    public Country? Country { get; set; }
    public List<Project>? Projects { get; set; } = new List<Project>();
}