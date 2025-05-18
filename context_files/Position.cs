using System.ComponentModel.DataAnnotations;
using BuildingBlock.Core.Domain.Abstractions;
using RSG.Biovision.Domain.Enums;

namespace RSG.Biovision.Domain.Entities;

public class Position : MainEntity
{
    [MaxLength(255)]
    public string? NameAr { get; set; }

    [Required]
    [MaxLength(255)]
    public string NameEn { get; set; }

    public string? DescriptionEn { get; set; }
    public string? DescriptionAr { get; set; }

    public Guid? SpecificationId { get; set; }

    public Specification? Specification { get; set; }
   
}